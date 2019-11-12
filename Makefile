.PHONY: build_container launch

build_container: .docker_installed /usr/bin/docker-compose
	pipenv lock -r > requirements.txt
	docker-compose build

launch:
	docker-compose up

/usr/bin/docker-compose:
	sudo curl -L "https://github.com/docker/compose/releases/download/1.24.1/docker-compose-$$(uname -s)-$$(uname -m)" -o /usr/bin/docker-compose
	sudo chmod +x /usr/bin/docker-compose

.docker_installed:
	sudo apt-get update
	sudo apt-get install -y \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg-agent \
    software-properties-common
	curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
	sudo apt-get update
	sudo add-apt-repository \
   "deb [arch=amd64] https://download.docker.com/linux/ubuntu disco stable"
	sudo apt-get install -y docker-ce docker-ce-cli containerd.io
	sudo gpasswd -a ${USER} docker
	exec su - ${USER}
	touch .docker_installed
