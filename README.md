PL:

Opis Projektu
Celem projektu było stworzenie aplikacji webowej umożliwiającej przeglądanie i filtrowanie danych o samochodach dostępnych na platformie otomoto.pl. Aplikacja korzysta z Flask jako frameworka webowego, SQLite jako bazy danych oraz Docker do zarządzania kontenerami. Parser zbudowany przy użyciu BeautifulSoup zbiera dane z zewnętrznej strony i przechowuje je w bazie danych.

Instrukcja Uruchomienia

Wymagania systemowe:

•	Docker

•	Docker Compose

Kroki do uruchomienia projektu

•	Sklonuj repozytorium:

      git clone https://github.com/AleksanderWyrwa/otomotoParser.git
   
•	Przejdź do katalogu projektu:

      cd ./projectDirectory/otomotoParser
   
•	Uruchom Docker Compose:

      docker-compose up --build

•	Połacz się z aplikacją:

      http://localhost:5000
 
ENG: 

Project Description
The goal of the project was to create a web application that allows users to browse and filter car data available on the otomoto.pl platform. The application uses Flask as the web framework, SQLite as the database, and Docker for container management. A parser built using BeautifulSoup collects data from the external site and stores it in the database.

System Requirements:

• Docker

• Docker Compose

Steps to Run the Project:

• Clone the repository:

     git clone https://github.com/AleksanderWyrwa/otomotoParser.git
  
• Navigate to the project directory:

     cd ./projectDirectory/otomotoParser
  
• Run Docker Compose:

     docker-compose up --build

• Connect to the application:

      http://localhost:5000
 
