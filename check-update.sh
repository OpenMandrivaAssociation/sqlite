#!/bin/sh
curl -L https://sqlite.org/ 2>/dev/null |grep Version |sed -e 's,.*">Version ,,;s,<.*,,'
