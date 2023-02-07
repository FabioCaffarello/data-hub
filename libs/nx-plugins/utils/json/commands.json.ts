import * as fs from 'fs';

export function readJson(filePath: string) {
  const jsonData = fs.readFileSync(filePath).toString();
  return JSON.parse(jsonData)
};

export function updateJson(filePath: string, json: any) {
  fs.writeFileSync(filePath, JSON.stringify(json, null, 2));
}
