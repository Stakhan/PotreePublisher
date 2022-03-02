# PotreePublisher
Small CLI to quickly publish a single LAS file or a whole folder to a Potree server.


## Prerequisites
It is assumed that you have a **Potree server** installed on your machine.
<details>
<summary>Expand for instructions if you don't :wink:</summary>

1. Clone the potree repository: `git clone https://github.com/potree/potree`

2. Make sure you have the Node Package Manager (npm) installed (usually delivered with node.js).

3. Inside potree's repository, run `npm install`. It will install dependencies (specified in package.json) and create a build in ./build/potree.

4. Move the potree folder to you favorite http server.

5. Make sure you spot the location where you want to:
 + store the point clouds
 + store the viewer html files

6. You're good to go! 
</details>

It is also assumed that you have **PotreeConverter** installed. See [this page](https://github.com/potree/PotreeConverter) for instructions.

## Installation
```
pip install potreepublisher
```

## Usage
```
Usage: PotreePublisher [OPTIONS] INPUT_PATH

Arguments:
  INPUT_PATH  Path to the point cloud or a folder of point clouds to process.
              Any type supported by PotreeConverter is possible.  [required]

Options:
  --potree-server-root TEXT  Root path of the potree server.  [default:
                             /var/www/potree]
  --point-cloud-folder TEXT  Folder where the point cloud will be stored after
                             conversion to Potree Format.  [default:
                             pointclouds]
  --viewer-folder TEXT       Folder where the viewer html page will be stored.
                             [default: results]
  --help                     Show this message and exit.
```
