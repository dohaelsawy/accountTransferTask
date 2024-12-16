build:
	docker build --tag web_image .
run:
	docker container run -it -p 8000:8000 --name web_container web_image
del_img:
	docker image rmi web_image --force
del_con:
	docker container rm web_container
delete-none-image-docker:
	docker rmi $(docker images --filter "dangling=true" -q --no-trunc)