
<!-- start badges -->

<a class="reference external image-reference" href="https://gitlab.com/benvial/geolia/-/releases" target="_blank"><img alt="Release" src="https://img.shields.io/endpoint?url=https://gitlab.com/benvial/geolia/-/jobs/artifacts/main/raw/logobadge.json?job=badge&labelColor=c9c9c9"></a> 
<a class="reference external image-reference" href="https://gitlab.com/benvial/geolia/commits/main" target="_blank"><img alt="Release" src="https://img.shields.io/gitlab/pipeline/benvial/geolia/main?logo=gitlab&labelColor=dedede&style=for-the-badge"></a> 
<a class="reference external image-reference" href="https://benvial.gitlab.io/geolia" target="_blank"><img alt="License" src="https://img.shields.io/badge/documentation-website-dedede.svg?logo=readthedocs&logoColor=e9d672&style=for-the-badge"></a>
<a class="reference external image-reference" href="https://gitlab.com/benvial/geolia/commits/main" target="_blank"><img alt="Release" src="https://img.shields.io/gitlab/coverage/benvial/geolia/main?logo=python&logoColor=e9d672&style=for-the-badge"></a>
<a class="reference external image-reference" href="https://black.readthedocs.io/en/stable/" target="_blank"><img alt="Release" src="https://img.shields.io/badge/code%20style-black-dedede.svg?logo=python&logoColor=e9d672&style=for-the-badge"></a>
<a class="reference external image-reference" href="https://gitlab.com/benvial/geolia/-/blob/main/LICENSE.txt" target="_blank"><img alt="License" src="https://img.shields.io/badge/license-GPLv3-blue?color=aec2ff&logo=open-access&logoColor=aec2ff&style=for-the-badge"></a>

<!-- end badges -->


# Geolia

**Geometry and mesh tools**

<!-- start elevator-pitch -->

- **Geometry and mesh definition helpers** --- Using the Gmsh Python API
- **Read meshes** --- Keeping track of physical domains with `meshio`
- **Interpolation** --- From unstructured to structured grids.


<!-- end elevator-pitch -->


## Documentation

See the website with API reference and some examples at [benvial.gitlab.io/geolia](https://benvial.gitlab.io/geolia).



<!-- start installation -->

## Installation


### From Pypi

Simply run

```bash 
pip install geolia
```

<!-- ### From conda/mamba


```bash 
mamba install -c conda-forge geolia
``` -->

### From source

Clone the repository

```bash 
git clone https://gitlab.com/benvial/geolia.git
```

Install the package locally

```bash 
cd geolia
pip install -e .
```


### From gitlab

```bash 
pip install -e git+https://gitlab.com/benvial/geolia.git#egg=geolia
```


<!-- end installation -->