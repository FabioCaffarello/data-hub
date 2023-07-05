import { BotWrapExecutorSchema } from './schema';
import executor from './executor';

const options: BotWrapExecutorSchema = {};

describe('BotWrap Executor', () => {
  it('can run', async () => {
    const output = await executor(options);
    expect(output.success).toBe(true);
  });
});