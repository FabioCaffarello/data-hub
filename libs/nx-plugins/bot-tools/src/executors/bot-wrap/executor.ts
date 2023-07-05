import { BotWrapExecutorSchema } from './schema';

export default async function runExecutor(
  options: BotWrapExecutorSchema,
) {
  console.log('Executor ran for BotWrap', options);
  return {
    success: true
  };
}

