# Variables
PROJECT_ID := vivek-dev-438315
BUCKET_NAME := resume-fit-web-server
BUILD_DIR := dist

# Build the Vue.js application
build: clean
	npm install
	npm run build

# Deploy to Google Cloud Storage
deploy: build clean-bucket
	gsutil -m rsync -r $(BUILD_DIR) gs://$(BUCKET_NAME)

# Set the bucket to be publicly accessible
make-public:
	gsutil iam ch allUsers:objectViewer gs://$(BUCKET_NAME)
	gsutil uniformbucketlevelaccess set on gs://$(BUCKET_NAME)
	gsutil web set -m index.html -e index.html gs://$(BUCKET_NAME)
	gsutil setmeta -h "Cache-Control:no-store, max-age=0" gs://$(BUCKET_NAME)/index.html
	gsutil stat gs://$(BUCKET_NAME)/index.html
	gsutil web get gs://$(BUCKET_NAME)

# Clean the build directory
clean:
	rm -rf $(BUILD_DIR)

# Clean the bucket
clean-bucket:
	gsutil -m rm -r gs://$(BUCKET_NAME)/**

check-favicon:
	gsutil cp gs://$(BUCKET_NAME)/favicon.ico /tmp/favicon_remote.ico
	diff $(BUILD_DIR)/favicon.ico /tmp/favicon_remote.ico


.PHONY: build deploy make-public clean clean-bucket
