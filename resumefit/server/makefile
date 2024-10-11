docker-build:
	cp ./build/Dockerfile.local Dockerfile
	docker build -t resume-fit-api-server .
	docker run -p 5000:10000 resume-fit-api-server

gcloud-build-deploy:
	rm -rf Dockerfile
	cp ./build/Dockerfile.gcloud Dockerfile
	docker build -t gcr.io/vivek-dev-438315/resume-fit-api-server .
	docker push gcr.io/vivek-dev-438315/resume-fit-api-server
	gcloud run deploy resume-fit-api-server --image gcr.io/vivek-dev-438315/resume-fit-api-server --platform managed --region asia-northeast1 --allow-unauthenticated