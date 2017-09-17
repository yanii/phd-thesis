#!/bin/sh
java -jar pdf1a/preflight-app-2.0.7.jar $1 > validation.txt
java -jar pdf1a/preflight-app-2.0.7.jar xml $1
