import { execSync } from 'child_process';

export function getCurrentGitUserName() {
  return execSync(`git config --get user.name`).toString('utf-8').trim()
}

export function getCurrentGitUserEmail() {
  return execSync(`git config --get user.email`).toString('utf-8').trim()
}
