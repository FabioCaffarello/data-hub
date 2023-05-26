export const networkName = 'data-hub-network';

export const stackTemplates = {
  mongodb: {
    image: 'mongo',
    ports: ['27017:27017'],
    volumes: ['./data:/data/db'],
    networks: [networkName],
  },
  rabbitmq: {
    image: 'rabbitmq:3-management',
    ports: ['5672:5672', '15672:15672'],
    environment: {
      RABBITMQ_DEFAULT_USER: 'guest',
      RABBITMQ_DEFAULT_PASS: 'guest',
      RABBITMQ_DEFAULT_VHOST: '/',
    },
    networks: [networkName],
  },
};
