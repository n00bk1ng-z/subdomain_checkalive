# Scanner
## Usage

目前只支持子域名扫描
使用之前可在OneForAll/config/api.py中修改api配置以获得更多结果

```bash
docker build . -t scanner:1.0
docker run -it --rm -v $(pwd):/app scanner:1.0 --target qq.com run
```

## TODO

- [ ] 增加端口扫描
- [ ] 增加漏洞扫描
- [ ] 增加指纹识别
