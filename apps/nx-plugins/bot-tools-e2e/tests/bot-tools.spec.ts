import {
  checkFilesExist,
  ensureNxProject,
  readJson,
  runNxCommandAsync,
  uniq,
} from '@nrwl/nx-plugin/testing';

describe('bot-tools e2e', () => {
  // Setting up individual workspaces per
  // test can cause e2e runs to take a long time.
  // For this reason, we recommend each suite only
  // consumes 1 workspace. The tests should each operate
  // on a unique project in the workspace, such that they
  // are not dependant on one another.
  beforeAll(() => {
    ensureNxProject('@data-hub/nx-plugins/bot-tools', 'dist/libs/nx-plugins/bot-tools');
  });

  afterAll(() => {
    // `nx reset` kills the daemon, and performs
    // some work which can help clean up e2e leftovers
    runNxCommandAsync('reset');
  });

  it('should create bot-tools', async () => {
    const project = uniq('bot-tools');
    await runNxCommandAsync(
      `generate @data-hub/nx-plugins/bot-tools:bot-tools ${project}`
    );
    const result = await runNxCommandAsync(`build ${project}`);
    expect(result.stdout).toContain('Executor ran');
  }, 120000);

  describe('--directory', () => {
    it('should create src in the specified directory', async () => {
      const project = uniq('bot-tools');
      await runNxCommandAsync(
        `generate @data-hub/nx-plugins/bot-tools:bot-tools ${project} --directory subdir`
      );
      expect(() =>
        checkFilesExist(`libs/subdir/${project}/src/index.ts`)
      ).not.toThrow();
    }, 120000);
  });

  describe('--tags', () => {
    it('should add tags to the project', async () => {
      const projectName = uniq('bot-tools');
      ensureNxProject('@data-hub/nx-plugins/bot-tools', 'dist/libs/bot-tools');
      await runNxCommandAsync(
        `generate @data-hub/nx-plugins/bot-tools:bot-tools ${projectName} --tags e2etag,e2ePackage`
      );
      const project = readJson(`libs/nx-plugins/${projectName}/project.json`);
      expect(project.tags).toEqual(['e2etag', 'e2ePackage']);
    }, 120000);
  });
});
