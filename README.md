# Denuncias
Desarrollo de tablero y resultado del proyecto de clasificacion de topicos sobre denuncias del gobierno. 

![Alt text](./pics/p_1_geo.png?raw=true "Pantalla Principal")

Detalle de la seleccion de barrio

Topico y mensualizada

![Alt text](./pics/p_02_geo.png?raw=true "Detalle")

# Deploy
## Docker image

continuumio/miniconda3:latest

Buil de la imagen

    sudo docker build -t denuncias .

![Alt text](./pics/size_image.png?raw=true "image")   

Run 
    
    sudo docker run -i -p 8080:8080 -d denuncias


### Tecnologias utilizadas
1. HTML
2. Javascript
3. Python 3.6
4. Flask


Tips a realizar para modificar el tamaño de la implementacion:
1. Pasar el dataframe a una DB 30mb menos.
2. Compilar el .py a un binario y sacar la instalacion de requerimientos.txt
3. Si se realiza el punto 2 cambiar la imagen por una mas chica con solamente dependencias del S.O