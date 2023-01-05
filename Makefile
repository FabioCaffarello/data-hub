# npx nx g @nrwl/nx-plugin:plugin python-tools --directory=nx-plugins --importPath=@data-hub/python-tools
#

dummie:
	echo Dummie

nx-create-plugin:
	npx nx g @nrwl/nx-plugin:plugin $(pluginName) --directory=nx-plugins --importPath=@data-hub/$(pluginName)

# nx-create-plugin-generator generatorName=create-project pluginName=python-tools
nx-create-plugin-generator:
	npx nx g @nrwl/nx-plugin:generator $(generatorName) --project=$(pluginName)

