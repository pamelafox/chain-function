# chain-function
An Azure function that generates a word from a Markov chain.

Endpoint:

```
https://pamelaschainfunction-apim.azure-api.net/PamelasChainFunction/ChainFunction
```

Query parameters:

* kind: (Required) A string specifying the chain to use. Supported value is "planet".
* seed: (Optional) An integer that will be used to seed the random number generator. The same seed will always yield the same result.

Usage in JavaScript:

```
let response = fetch("https://pamelaschainfunction-apim.azure-api.net/PamelasChainFunction/ChainFunction?kind=planet", {
headers: {
    "Ocp-Apim-Subscription-Key": "<KEY HERE>",
  }
}).then((response) => response.text())
.then(console.log)
.catch(console.error);
```