import {
  Tree,
} from '@nrwl/devkit';
import { readJson, updateJson } from '../../../../utils/json/commands.json';
import { FixDockerConfigGeneratorSchema } from './schema';
import { expect } from '@jest/globals';


const filePath = '../.docker/config.json'

export default async function (tree: Tree, options: FixDockerConfigGeneratorSchema) {

  const configData = readJson(filePath)
  delete configData.credsStore;
  updateJson(filePath, configData);
}

export function assertGenerateFiles(tree: Tree) {
  const config = readJson(filePath);
  expect(config.credsStore).toBeUndefined();
}
