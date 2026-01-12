# CarePath Runbook (Operations)

This runbook explains how the service is deployed and how to troubleshoot it.

## Service
- Live URL: http://130.162.244.205:8000
- Health endpoint: http://130.162.244.205:8000/health

## Deployment model
- CI builds and tests the application.
- CD builds a container image and pushes to GHCR.
- Server deploy uses Podman (Oracle Linux 9) to pull and run the latest image.

## On-server commands (Oracle Linux 9)
### Check service status
```bash
podman ps
curl -s http://localhost:8000/health
