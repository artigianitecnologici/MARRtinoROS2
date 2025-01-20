sudo sshpass -p 'PwdMrt2022@' ssh -N \
    -R 51.75.22.208:8022:localhost:22 \
    -R 51.75.22.208:8080:localhost:80 \
    -R 51.75.22.208:8085:localhost:8085 \
    marrtino@51.75.22.208 -o "StrictHostKeyChecking no"
