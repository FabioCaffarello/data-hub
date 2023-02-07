import {
  Tree,
} from '@nrwl/devkit';
import * as path from 'path';
import { readJson, updateJson } from '../../../../utils/json/commands.json';
import { FixDockerConfigGeneratorSchema } from './schema';


export default async function (tree: Tree, options: FixDockerConfigGeneratorSchema) {
  const filePath = '../.docker/config.json'
  const configData = readJson(filePath)
  delete configData.credsStore;
  updateJson(filePath, configData);
}
