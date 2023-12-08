# Additional Arguments

## callback

`--callback` is an optional argument which POSTs JSON data that has
the status of the test, at the end of the test to the given URL. The
URL should be a valid http(s) link that accepts POST data.

[See Callbacks Reference, for more details](../../callbacks.md)

## host

`host` is an optional argument which allows user to run the test on a different host Runner. Valid values are 'x86_64', 'm6a.large', 'm6g.large', 'm6id.large', 'm6gd.large'. 'x86_64' is the default value.

* **x86_64 is 2vCPU + 4GB RAM with swap**
* **m6a.large is 2vCPU + 8GB RAM with no swap**
* **m6g.large is 2vCPU + 8GB RAM with no swap**
* **m6id.large is 2vCPU + 8GB RAM with NVMe disk and no swap**
* **m6gd.large is 2vCPU + 8GB RAM with NVMe disk and no swap**

```
tuxsuite test --device qemu-armv7 --kernel https://storage.tuxboot.com/armv7/zImage --tests boot,ltp-smoke --host x86_64_large
```
