#pragma once

#include <cmath>
#include <iostream>

class Vec3{
    public:
        double e[3];

        Vec3() : e{0,0,0}{}
        Vec3(double e0, double e1, double e2) : e{e0, e1, e2}{}

        double x() const { return e[0]; }
        double y() const { return e[1]; }
        double z() const { return e[2]; }

        Vec3 operator - () const { return Vec3(-e[0], -e[1], -e[2]); }
        double operator [] (int i) const { return e[i]; }
        double & operator [] (int i) {return e[i]; }

        Vec3 & operator += (const Vec3 & other){
            this->e[0] += other.e[0];
            this->e[1] += other.e[1];
            this->e[2] += other.e[2];
            return *this;
        }

        Vec3 & operator *= (double C){
            this->e[0] *= C;
            this->e[1] *= C;
            this->e[2] *= C;
            return *this;
        }

        Vec3 & operator /= (double t){
            return *this *= 1/t;
        }

        double length() const {
            return sqrt(length_squared());
        }

        double length_squared() const {
            return this->e[0]*this->e[0] + this->e[1]*this->e[1] + this->e[2]*this->e[2];
        }
};

// point3 is just an alias for vec3, but useful for geometric clarity in the code.
using Point3 = Vec3;

// Vector Utility Functions

inline std::ostream & operator << (std::ostream & out, const Vec3 & o){
    return out << o.e[0] << ' ' << o.e[1] << ' ' << o.e[2];
}

//------------------------------------------------------------------

inline Vec3 operator + (const Vec3 & v, const Vec3 & o){
    return Vec3(v.e[0] + o.e[0], v.e[1] + o.e[1], v.e[2] + o.e[2]);
}

inline Vec3 operator + (const Vec3 & v, double scalar){
    return Vec3(v.e[0] + scalar, v.e[1] + scalar, v.e[2] + scalar);
}

inline Vec3 operator + (double scalar, const Vec3 & v){
    return v + scalar;
}

//------------------------------------------------------------------

inline Vec3 operator - (const Vec3 & v, const Vec3 & o){
    return Vec3(v.e[0] - o.e[0], v.e[1] - o.e[1], v.e[2] - o.e[2]);
}

inline Vec3 operator - (const Vec3 & v, double scalar){
    return Vec3(v.e[0] - scalar, v.e[1] - scalar, v.e[2] - scalar);
}

inline Vec3 operator - (double scalar, const Vec3 & v){
    return v - scalar;
}

//------------------------------------------------------------------

inline Vec3 operator * (const Vec3 & v, double scalar){
    return Vec3(v.e[0] * scalar, v.e[1] * scalar, v.e[2] * scalar);
}

inline Vec3 operator * (double scalar, const Vec3 & v){
    return Vec3(v.e[0] * scalar, v.e[1] * scalar, v.e[2] * scalar);
}

//------------------------------------------------------------------

inline Vec3 operator / (const Vec3 & v, double scalar){
    return (1/scalar) * v;
}

//------------------------------------------------------------------

inline double dot(const Vec3 & v, const Vec3 & u){
    return    v.e[0] * u.e[0]
            + v.e[0] * u.e[0]
            + v.e[0] * u.e[0];
}

inline Vec3 cross(const Vec3 & v, const Vec3 & u){
    return Vec3(
        u.e[1] * v.e[2] - u.e[2] * v.e[1],
        u.e[2] * v.e[0] - u.e[0] * v.e[2],
        u.e[0] * v.e[1] - u.e[1] * v.e[0]
    );
}

inline Vec3 unit_vector(const Vec3 & v){
    return v / v.length();
}