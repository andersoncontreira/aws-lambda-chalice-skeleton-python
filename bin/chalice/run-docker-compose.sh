# Usage: up [options] [--scale SERVICE=NUM...] [SERVICE...]
#
# Options:
#-d, --detach               Detached mode: Run containers in the background,
#                               print new container names. Incompatible with
#                               --abort-on-container-exit.
#    --no-color                 Produce monochrome output.
#    --quiet-pull               Pull without printing progress information
#    --no-deps                  Don't start linked services.
#    --force-recreate           Recreate containers even if their configuration
#                               and image haven't changed.
#    --always-recreate-deps     Recreate dependent containers.
#                               Incompatible with --no-recreate.
#    --no-recreate              If containers already exist, don't recreate
#                               them. Incompatible with --force-recreate and -V.
#    --no-build                 Don't build an image, even if it's missing.
#    --no-start                 Don't start the services after creating them.
#    --build                    Build images before starting containers.
#    --abort-on-container-exit  Stops all containers if any container was
#                               stopped. Incompatible with -d.
#    -t, --timeout TIMEOUT      Use this timeout in seconds for container
#                               shutdown when attached or when containers are
#                               already running. (default: 10)
#    -V, --renew-anon-volumes   Recreate anonymous volumes instead of retrieving
#                               data from the previous containers.
#    --remove-orphans           Remove containers for services not defined
#                               in the Compose file.
#    --exit-code-from SERVICE   Return the exit code of the selected service
#                               container. Implies --abort-on-container-exit.
#    --scale SERVICE=NUM        Scale SERVICE to NUM instances. Overrides the
#                               `scale` setting in the Compose file if present.
# ---------------------------
# $1 options
docker-compose -f docker-compose-chalice.yml up $1
