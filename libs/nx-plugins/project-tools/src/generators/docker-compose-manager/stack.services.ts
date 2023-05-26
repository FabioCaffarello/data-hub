export const propsMappings = {
  bot: 'botService',
  backend: 'backendService',
  frontend: 'frontendService',
};

export const serviceProps = {
  botService: false,
  backendService: false,
  frontendService: false,
};

export const stackMappings = {
  bot: [
    "mongodb",
    "rabbitmq"
  ]
}
