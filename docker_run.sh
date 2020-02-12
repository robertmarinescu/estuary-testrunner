docker run  -p 8080:8080 -v "$PWD/inputs/templates:/data"  -v "$PWD/inputs/variables:/variables" -v /var/run/docker.sock:/var/run/docker.sock dinutac/estuary-testrunner:latest
