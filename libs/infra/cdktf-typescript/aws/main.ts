// Copyright (c) HashiCorp, Inc
// SPDX-License-Identifier: MPL-2.0
import { Construct } from "constructs";
import { App, TerraformOutput, TerraformStack } from "cdktf";
import { AwsProvider } from "@cdktf/provider-aws/lib/provider"
import { KeyPair } from "@cdktf/provider-aws/lib/key-pair"
import { Instance } from "@cdktf/provider-aws/lib/instance";
import * as fs from "fs";

class MyStack extends TerraformStack {
  constructor(scope: Construct, id: string) {
    super(scope, id);

    const pubKey = fs.readFileSync("cdktftempkey.pub", "utf-8");

    new AwsProvider(this, "aws", {
      region: "us-east-1",
    });

    const keyPair = new KeyPair(this, "keypair", {
      keyName: "cdktftempkey",
      publicKey: pubKey,
    });

    const machine = new Instance(this, "machine", {
      ami: "ami-00874d747dde814fa",
      instanceType: "t2.micro",
      keyName: keyPair.keyName,
    });

    new TerraformOutput(this, "public_ip", {
      value: machine.publicIp,
    });
  }
}

const app = new App();
new MyStack(app, "temp");
app.synth();
