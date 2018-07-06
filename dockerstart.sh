docker run --mount type=bind,source=/home/ubuntu/pleroma.db,target=/pleroma/pleroma.db --env-file .env -it -p80:80 -d pleromanna:local
