FROM python
COPY . .

RUN pip install -r req.txt

CMD python main.py