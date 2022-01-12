# PotreePublisher
Small CLI to quickly publish a single LAS file or a whole folder to a Potree server.
```
Usage: PotreePublisher [OPTIONS] INPUT_POINT_CLOUD

Arguments:
  INPUT_POINT_CLOUD  Path to the point cloud to process. Any type supported by
                     PotreeConverter is possible.  [required]

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
