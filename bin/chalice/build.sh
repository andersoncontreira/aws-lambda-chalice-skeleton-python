# execute from the root of the project

# remove the last image
docker rmi -f project-name-chalice

# create the image
docker build -t project-name-chalice -f ./environment/chalice/Dockerfile .