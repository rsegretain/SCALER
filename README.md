# Smart Group Scaling for Webscale Microservice Applications

# Files structure

- global-resources
	- load-profiles : csv files and the tool to generate them
	- plot_utils.py : commons functions used to plot
	- wrk3-commons + template : commons function for wrk3 Lua scripts
	- metric server manifest : required for the HPA
	- json.lua : Lua lib used to saved data required to send requests to applications, like login token.
	- istio manifests
	- K8S configs/version
	-autoscaler scripts

-<APP>
	- experiment conf :
		- saturation value per services/endpoint
		- wrk3 parameter (nb of connections/threads)
		- load script used
		- specific parameters
		- load profile used for warmup
	- global parameters used in experiments
	- application manifests
	- plot.py + pip3 module requirement
	- wrk3 Lua scripts
	- istio load balancer manifest
	- HPA manifest

# Results data set

Experiments results data are available at the following link while paper is under review and will be uploaded to proper scientific platform if/when the paper is accepted :
- [https://www.grosfichiers.com/2ZXAgwg2cHD](https://www.grosfichiers.com/2ZXAgwg2cHD)

# Load generator

wrk3, the HTTP requests generator is available here : [https://open-science.anonymous-github.xyz/r/wrk3-7444](https://open-science.anonymous-github.xyz/r/wrk3-7444)