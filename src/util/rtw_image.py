from PIL import Image
import numpy as np
import os

class rtw_image:
    def __init__(self):
        self.fdata = None  # Linear floating point pixel data [0.0, 1.0]
        self.bdata = None  # Linear 8-bit pixel data [0, 255]
        self.image_width = 0
        self.image_height = 0
        self.bytes_per_pixel = 3  # RGB
        self.bytes_per_scanline = 0
    
    @classmethod
    def from_file(cls, image_filename: str) -> "rtw_image":
        """
        Loads image data from the specified file. If the RTW_IMAGES environment 
        variable is defined, looks only in that directory for the image file. 
        If the image was not found, searches for the specified image file first 
        from the current directory, then in the images/ subdirectory, then the 
        parent's images/ subdirectory, and so on, for six levels up.
        """
        instance = cls()
        
        imagedir = os.environ.get("RTW_IMAGES")
        
        # Hunt for the image file in some likely locations
        search_paths = []
        if imagedir:
            search_paths.append(os.path.join(imagedir, image_filename))
        
        search_paths.append(image_filename)
        search_paths.append(f"images/{image_filename}")
        for i in range(1, 7):
            prefix = "../" * i
            search_paths.append(f"{prefix}images/{image_filename}")
        
        for path in search_paths:
            if instance.load(path):
                return instance
        
        print(f"ERROR: Could not load image file '{image_filename}'.")
        return instance
    
    def load(self, filename: str) -> bool:
        """
        Loads the linear (gamma=1) image data from the given file name. 
        Returns true if the load succeeded. The resulting data buffer contains 
        the three [0.0, 1.0] floating-point values for the first pixel 
        (red, then green, then blue). Pixels are contiguous, going left to right 
        for the width of the image, followed by the next row below, for the full 
        height of the image.
        """
        try:
            img = Image.open(filename).convert("RGB")
        except (FileNotFoundError, OSError):
            return False
        
        self.image_width, self.image_height = img.size

        # Convert to numpy array and normalize to [0.0, 1.0]
        self.fdata = np.array(img, dtype=np.float32) / 255.0

        # Convert from sRGB (gamma-encoded) to linear color space
        # JPEGs are stored in sRGB, but raytracing works in linear space
        # We use gamma=2.0 here to match the output gamma correction (sqrt = gamma 2.0)
        # self.fdata = np.power(self.fdata, 2.0)

        # Convert to bytes [0, 255]
        self._convert_to_bytes()
        
        return True
    
    def width(self) -> int:
        return 0 if self.fdata is None else self.image_width
    
    def height(self) -> int:
        return 0 if self.fdata is None else self.image_height
    
    def pixel_data(self, x: int, y: int) -> tuple[int, int, int]:
        """
        Return the three RGB byte values of the pixel at x,y. 
        If there is no image data, returns magenta.
        """
        if self.bdata is None:
            return (255, 0, 255)  # magenta
        
        x = self._clamp(x, 0, self.image_width)
        y = self._clamp(y, 0, self.image_height)
        
        return tuple(self.bdata[y, x])
    
    def pixel_data_float(self, x: int, y: int) -> tuple[float, float, float]:
        """
        Return the three RGB float values [0.0, 1.0] of the pixel at x,y.
        If there is no image data, returns magenta.
        """
        if self.fdata is None:
            return (1.0, 0.0, 1.0)  # magenta
        
        x = self._clamp(x, 0, self.image_width)
        y = self._clamp(y, 0, self.image_height)
        
        return tuple(self.fdata[y, x])
    
    @staticmethod
    def _clamp(x: int, low: int, high: int) -> int:
        """Return the value clamped to the range [low, high)."""
        if x < low:
            return low
        if x < high:
            return x
        return high - 1
    
    @staticmethod
    def _float_to_byte(value: float) -> int:
        """Convert a [0.0, 1.0] float to a [0, 255] byte."""
        if value <= 0.0:
            return 0
        if value >= 1.0:
            return 255
        return int(256.0 * value)
    
    def _convert_to_bytes(self):
        """
        Convert the linear floating point pixel data to bytes, 
        storing the resulting byte data in the bdata member.
        """
        # Vectorized conversion using numpy
        self.bdata = np.clip(self.fdata * 256.0, 0, 255).astype(np.uint8)