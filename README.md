<h1><font style=text-decoration: underline;>Docker and HZZ</font></h1>
<div name="description">
	<h2 style=text-decoration: underline;>Description</h2>
	<p>
	In this repository, I play around with the HZZ analysis notebook. I strip the various functions from the notebook as if they were modules and put them in 2 different containers. <br/>
		<h3>The containers</h3>
		<ul>
			<li>Get_data</li>
			<li>Plot_data</li>
		</ul>
	The <strong>Get_data</strong> container grabs data from the public servers and processes it into a dataframe, a list and an array.<br/>
	Then sends all of them as pickle dumps to be received by the plot_data container. The information is sent as messages using RabbitMQ. <br/>
	<strong>Plot_data</strong> then has code that processes the dataframe, list and array and then plots the received data, then saves the data as a plot named 'plot_dd_mm_yy-HH-MM.png'.<br/>
	This can then be retreived from the plot_data container using the docker cp command.
	</p>
	<h2 style=text-decoration: underline;>Building the images</h2>
	<p>Building the images is very easy, the Dockerfile is included in the folders of the respective code scripts to build images. After navigating to the folders where the respective code is,<br/> you have to do the following.</p>
	<p>For get_data image:</p>

```bash
docker image build -t get_data .
```

<p>For plot_data image:</p>

```bash
docker image build -t plot_data .
```

<h2 style=text-decoration: underline;>Building the containers</h2>
	<p>Building the containers is a little different than containers, the image is already in the local docker repository. We just need to be careful to add arguments carefully.<br/>
<p>For plot_data(named as plot_d1) image:</p>

```bash
docker run --name get_d1 -it -P get_data
```
 <span style=border: 2px solid red; border-radius: 5px; border-style: dashed;>
	-it: adds interactive shell<br/>
	-P: maps ports randomly<br/>
	-d: detaches the container from the CLI (runs it in background) <br/>
	In this case you can see the logs by using:</span>
 </p>
 
```bash
docker logs get_d1 -f
```

<p>Here the -f follows the output of the container as it works.</p>

<p>For plot_data(named as plot_d1) image:</p>

```bash
docker run --name plot_d1 -it -P plot_data
```



</div>
