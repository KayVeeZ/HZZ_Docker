<h1><font style=text-decoration: underline;>Docker and HZZ</font></h1>
<div name="description">
	<h2 style=text-decoration: underline;>Description</h2>
	<p>
	In this repository, I play around with the HZZ analysis notebook. I strip the various functions from the notebook as if they were modules <br/>
	and put them in 2 different containers. <br/>
		<h3>The containers</h3>
		<ul>
			<li>Get_data</li>
			<li>Plot_data</li>
		</ul>
	The Get_data container grabs data from the public servers and processes it into a dataframe, a list and an array.<br/>
	Then sends all of them as pickle dumps to be received by the plot_data container. The information is sent as messages using RabbitMQ. <br/>
	Plot_data then has code that processes the dataframe, list and array and then plots the received data, then saves the data as 'plot_dd_mm_yy-HH-MM.png'.<br/>
	This can then be retreived from the plot_data container using the docker cp command.
	</p>
</div>

