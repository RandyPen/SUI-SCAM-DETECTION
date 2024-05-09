const mainnet = "https://fullnode.mainnet.sui.io:443";

// let server = Bun.serve({
//   async fetch(req) {
//     const fakeheaders = req.headers;
//     fakeheaders.set("host", "https://fullnode.mainnet.sui.io");
//     console.log(req);
//     const response = await fetch(mainnet, {
//       method: req.method,
//       body: req.body,
//       headers: fakeheaders,
//     });
//     console.log(response);
//     return response;
//   },
// });

import express from "express";
import { createProxyMiddleware } from "http-proxy-middleware";

const app = express();
const port = 3000;

app.use(
  "/",
  createProxyMiddleware({
    target: "https://fullnode.mainnet.sui.io",
    changeOrigin: true,
    secure:false,
    on: {
      proxyReq: (proxyReq, req, res) => {
        /* handle proxyReq */
                let data: Uint8Array[] = [];
                let body = ''
                req.on("data", (chunk) => {
                  data.push(chunk);
                });
                req.on("end", () => {
                  body = Buffer.concat(data).toString();
                  console.log("body:", body);
                  // At this point, `body` has the entire request payload stored in it as a string
                });
        proxyReq.setHeader('Access-Control-Allow-Origin','*');
        
        //console.log(req.headers);
      },
      proxyRes: (proxyRes, req, res) => {
        /* handle proxyRes */
        proxyRes.headers["access-control-allow-headers"] = "*";

      },
      error: (err, req, res) => {
        /* handle error */
        console.log(err);
      },
    },
  })
);


app.listen(port);
