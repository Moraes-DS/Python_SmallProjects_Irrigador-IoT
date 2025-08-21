# Python_SmallProjects_Irrigador-IoT
Irrigador automático com Raspberry Pi, que monitora a umidade do solo por sensor e aciona a bomba d’água de forma inteligente. Projeto em Python, com uso de GPIO e callbacks, promove automação eficiente e economia de água no cultivo de pequenas verduras em locais sem fonte de água próxima. Ideal para apartamentos.

1) Verifica se está no horário ativo (8h > horário ativo < 21h);
2) Identifica se há água suficiente no reservatório;
  A1) Reservatório com Água (led vermelho desligado, led verde ligado)
  A2) Verifica se o solo está seco;
    Solo seco --> Inicia a irrigação (led amarelo desligado);
    Liga bomba d'água (led verde piscando);
    Aguarda tempo para a próxima irrigação;

    Solo úmido --> Aguarda tempo até o solo secar (led amarelo ligado);
    Retorna à verificação de umidade do solo;

  B1) Reservatório sem água (led vermelho aceso e led verde apagado);
  B2) Esperando o refil da água no reservatório;

