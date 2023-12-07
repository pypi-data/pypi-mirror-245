# LV-Physics: A common computational toolkit for LineVision physics and math

This Python package is intended to become the common code for handling physical and mathematical computations at
LineVision. It is meant to be easily installable by other LineVision applications, such as data pipeline microservices
as well as R&D code for technical analyis.

LV-Physics Computational Tools:
- 3D-Vector basic operations (cross, dot, mag, unit)
- 3D-Vector rotations (setup and apply rotations, basic rotations about an axis, rotation matrices)
- EMF modeling (electric and magnetic fields around OHLs)

To get an idea of how LV-Physics works and what it can do, please check out our Jupyter Lab
[tutorials](./extras/tutorials/).

## Python Version

We are currently using `3.11.1`. We recommend using `pyenv` to manage your python builds, and Python's `venv` to manage
your virtual environment.

## Installation

### Using PIP and AWS CodeArtifact

This package is published in LineVision's CodeArtifact repository. It is therefore easy to install using `pip`, but it
will require some setup of AWS.

#### Setting up AWS

1. Install the AWS CLI by following the
   [official installation guide](https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2.html).

2. Configure the AWS CLI with your AWS credentials by running:

   ```
   aws configure
   ```

   Enter your AWS Access Key ID, AWS Secret Access Key, Default region name, and Default output format as prompted.

#### Installing using AWS CodeArtifact

1. Log in to AWS CodeArtifact by running:

   ```
   aws-login "aws codeartifact login --tool pip --domain linevision-dev --repository dev-linevision-pip"
   ```

   Note that you must log in every 24 hours to maintain access to the repository.

2. Install the LV-Physics package using pip:

   ```
   pip install lv-physics
   ```

### For Developers

#### Using the Makefile

The Makefile contains several useful commands for development work within the LV-Physics package:

- `make build-env`: Set up the Python virtual environment and install the necessary tools.
- `make install`: Install the package and its dependencies.
- `make test`: Run tests for the package.
- `make clean`: Clean up the environment, removing build artifacts and other temporary files.
- `make reset`: Cleans and builds the environment, and installs the package into the local venv.

#### Publishing with Flit and bumping the version

1. Build the environment and install the package.

   ```
   make build-env
   make install-pkg  
   ``` 

2. Use the Makefile to bump the version, at the appropriate level `major.minor.patch`.

   ```
   make bump-{LEVEL}  
   ```

3. Publish to AWS CodeArtifact.

   ```
   make publish
   ```

## The Vector Philosophy of LV-Physics

In our work at LineVision, we often deal with 3D geometric calculations, which can be complex and hard to manage. The
"vector" is a powerful mathematical tool that simplifies these calculations, providing several advantages:

- Brevity: Vector notation condenses complex expressions, making calculations easier to understand and perform
- Flexibility: Vectors let us work without depending on a specific coordinate system, increasing adaptability
- Intuitive representation: Vectors naturally represent physical quantities like forces, velocities, and displacements
- Reduced errors: By simplifying calculations, vector notation decreases the chances of errors from handling components
- Enhanced readability: Vectors improve collaboration and communication through concise, universally understood notation

A vector, denoted as $\vec{v}$, represents both magnitude and direction in 3D space. It can be written as 
$\vec{v} = (v_x, v_y, v_z)$, where the components depend on the coordinate system. However, with vectors, we can perform
calculations without focusing on individual components.

Vectors are versatile mathematical entities that can represent a wide variety of physical quantities in an intuitive and
concise manner. Here are some examples of entities that can be represented using vectors:

1. **Position**: A position vector, $\vec{r}$, can describe the location of a point in space relative to a reference
   point, often called the origin. In 3D space, the position vector can be represented as:

   $$\vec{r} = (x, y, z)$$

   where x, y, and z are the coordinates of the point along the x, y, and z axes, respectively.

2. **Displacement**: A displacement vector, $\vec{d}$, represents the change in position between two points, A and B. It
   is defined as the difference between their position vectors, $\vec{r}_B$ and $\vec{r}_A$:

   $$\vec{d} = \vec{r}_B - \vec{r}_A$$

3. **Axis of rotation**: Vectors can also represent the axis of rotation for a 3D object. A unit vector, $\hat{n}$,
   along the axis of rotation can be used to describe the orientation of the rotational axis. For example, if we have
   two vectors $\vec{u}$ and $\vec{v}$, and we wish to rotate the vector $\vec{u}$ into $\vec{v}$, we rotate about the
   axis obtained from their cross product, perpendicular to both:

   $$\hat{n} = \hat{u} \times \hat{v}$$

  $$
  \vec{v}_{rot} = \vec{v} \cos(\theta) + (\vec{n} \times \vec{v}) \sin(\theta)
                + \vec{n}(\vec{n} \cdot \vec{v})(1 - \cos(\theta))
  $$

4. **Field vectors**: Vectors are commonly used to represent field quantities, such as the magnetic field, $\vec{B}$.
   The field vector at a specific point in space indicates the field's strength and direction at that location. For
   example, the magnetic field vector around a straight current-carrying wire can be represented by the Biot-Savart law:

   $$\vec{B} = \frac{\mu_0}{4\pi}\frac{\vec{I}\ \times \vec{r}}{r^2}$$

   where $\mu_0$ is the permeability of free space, $\vec{I} is the current vector and $\vec{r}$ is the position vector
   from the wire to the point of interest.

Embracing the vector philosophy in LV-Physics significantly enhances the efficiency, readability, and adaptability of
our mathematical and physical models and calculations.

### Vectors and N-Vectors in Python

The `numpy` library was taylor-made for handling 3-dimensional vectors (and their higher dimensional analogs) in Python.
We may also have a collection of N vectors that we want to operate on. The following convention in `lv-physics` is used
to work with a a single 3-dimensional vector, and the collection of N 3D-vectors - an 'N-vector'.

* A 3D vector will always be represented by a `numpy.ndarray` of length 3:

```
a_vector = np.array([3.0, 5.0, 8.0])

# Selecting vector components
a_x = a_vector[0]
a_y = a_vector[1]
a_z = a_vector[2]
```

* An N-vector, a collection of N 3D vectors, will always be represented by a `numpy.ndarray` of shape (N, 3):

```
n_vectors = np.array(
    [
        [1.0, 2.0, 4.0],
        [3.0, 5.0, 8.0],
    ]
)
```

A prime example for the usage of N-vectors is with a set of N LiDAR points in a scan.

```
points = lidar_interface.points

# Grabbing a single LiDAR point
the_77th_point = points[77]

# Grabbing all of the components of the entire LiDAR scan
all_x_components = points[:, 0]
all_y_components = points[:, 1]
all_z_components = points[:, 2]
```

**!IMPORTANT!**: In `lv-physics`, we always treat 3D vectors as being in the conventional order of (x, y, z) for
cartesian coordinates, and (r, az, el) for spherical coordinates, obeying the right-handed coordinate convention. Take
care to always instantiate vector arrays using this convention when using main `lv-physics` modules directly.
