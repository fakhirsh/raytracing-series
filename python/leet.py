from typing import List

class Solution:
    def findAllPeople(self, n: int, meetings: List[List[int]], firstPerson: int) -> List[int]:
        """
        Ultra-optimized Union-Find solution with path compression and union by rank.
        
        This approach uses a persistent Union-Find structure with smart reset strategy,
        achieving near-linear time complexity O(M log M + M·α(N)) where α is the inverse
        Ackermann function (effectively constant for practical purposes).
        """
        # Persistent Union-Find with path compression and union by rank
        parent = list(range(n))
        rank = [0] * n
        
        def find(x):
            if parent[x] != x:
                parent[x] = find(parent[x])  # Path compression
            return parent[x]
        
        def union(x, y):
            px, py = find(x), find(y)
            if px != py:
                # Union by rank for optimal tree height
                if rank[px] < rank[py]:
                    px, py = py, px
                parent[py] = px
                if rank[px] == rank[py]:
                    rank[px] += 1
        
        # Person 0 and firstPerson know the secret initially
        union(0, firstPerson)
        
        # Sort meetings by time (O(M log M))
        meetings.sort(key=lambda x: x[2])
        
        i = 0
        while i < len(meetings):
            # Collect all meetings at the same time
            current_time = meetings[i][2]
            people_at_time = []
            
            # Process all meetings at this time slot
            while i < len(meetings) and meetings[i][2] == current_time:
                x, y = meetings[i][0], meetings[i][1]
                union(x, y)
                people_at_time.append(x)
                people_at_time.append(y)
                i += 1
            
            # Smart reset: only reset people who aren't connected to person 0
            # This is the key insight - we don't need to rebuild everything
            for person in people_at_time:
                if find(person) != find(0):  # Not connected to secret source
                    parent[person] = person  # Reset this person
                    rank[person] = 0
        
        # Return all people connected to person 0 (who know the secret)
        return [i for i in range(n) if find(i) == find(0)]

# Test cases with performance benchmarking
if __name__ == "__main__":
    import time
    
    solution = Solution()
    
    # Test cases from the problem
    test_cases = [
        (6, [[1,2,5],[2,3,8],[1,5,10]], 1, [0,1,2,3,5]),
        (4, [[3,1,3],[1,2,2],[0,3,3]], 3, [0,1,3]),
        (5, [[3,4,2],[1,2,1],[2,3,1]], 1, [0,1,2,3,4]),
    ]
    
    print("Testing Union-Find optimized solution:")
    for i, (n, meetings, firstPerson, expected) in enumerate(test_cases, 1):
        start = time.time()
        result = solution.findAllPeople(n, meetings, firstPerson)
        end = time.time()
        
        result_sorted = sorted(result)
        expected_sorted = sorted(expected)
        
        status = "✓" if result_sorted == expected_sorted else "✗"
        print(f"Test {i}: {result_sorted} {status} (Time: {(end-start)*1000:.3f}ms)")
    
    # Large performance test
    print("\nLarge performance test:")
    n_large = 100000
    meetings_large = []
    for i in range(500000):
        meetings_large.append([i % n_large, (i + 1) % n_large, i // 100])
    firstPerson_large = 50000
    
    start = time.time()
    result_large = solution.findAllPeople(n_large, meetings_large, firstPerson_large)
    end = time.time()
    
    print(f"Large test: {len(result_large)} people know the secret (Time: {(end-start)*1000:.3f}ms)")
    
    # Edge case tests
    print("\nEdge case tests:")
    
    # Single meeting
    result = solution.findAllPeople(2, [[0, 1, 1]], 1)
    print(f"Single meeting: {sorted(result)} (Expected: [0,1])")
    
    # No meetings
    result = solution.findAllPeople(5, [], 3)
    print(f"No meetings: {sorted(result)} (Expected: [0,3])")
    
    # All meetings at same time
    result = solution.findAllPeople(4, [[0,1,1],[1,2,1],[2,3,1]], 1)
    print(f"Same time meetings: {sorted(result)} (Expected: [0,1,2,3])")


 