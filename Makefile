
nx-create-plugin:
	npx nx g @nrwl/nx-plugin:plugin $(pluginName) --directory=nx-plugins --importPath=@data-hub/$(pluginName)

nx-create-plugin-generator:
	npx nx g @nrwl/nx-plugin:generator $(generatorName) --project=$(pluginName)

# npx nx run shared-python-tools-core:add --name shared-python-tools-development --group=dev --local
