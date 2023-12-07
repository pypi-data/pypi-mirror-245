# qamlib

This is a library meant to be an easy way to interact with a V4L2 camera, by
having a simple interface to capture images, and setup the camera. It is a
C++20 class (+ a few structs) together with optional Python bindings via
`pybind11`.

Do note that we currently don't really use or test the pure C++ build, so that
might not be working entirely and will likely be lacking quite a bit of polish.

The Python bindings are the main usage of `qamlib`, so the C++ API is a bit of
a secondary concern.

There are also some features supported that are currently exclusive to
Qtechnology A/S cameras, but these are not compiled when main-line kernel
headers are detected.

## Example

```python
import qamlib

cam = qamlib.Camera("/dev/video0")

# Use context manager to start and stop streaming
with cam:
    metadata, frame = cam.get_frame() # gets an image as raw bytes
    # process image
```

See more in the
[documentation](https://qtec.gitlab.io/software/distro/camera_utilities/qamlib/index.html)

## Building

### Python

Dependencies

- `gcc`
- `libstdc++-dev`
- `nlohmann-json`
- `pybind11_json`
- `python3-dev`
- `pybind11`
- `setuptools`

To build the module:

```sh
python setup.py build
```

To install the module (this also builds the module):

```sh
pip install .
```

### C++

Dependicies

- `gcc`
- `meson`
- `ninja`
- `nlohmann-json`

To build the library we start by running `meson` setup:

```sh
meson setup build
```

Then to compile do

```sh
cd build
meson compile
```

To install the package, run (this also builds the library):

```sh
meson install
```

## Testing

Under `tests/` are some tests, these have only been actually tested on
Qtechnology A/S cameras.
