
#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <cctype>
using namespace std;



vector<string> keywords = {"str","char","int","for","in","if",};

vector<string> nom_funciones = {"crack", "mvp", "localiza","saca","wachea"};

vector<char> simbolos = {'(',')','{','}','+',','};

bool saberSiKeyword(string dato){
  bool encontrado = false;
  for (int i = 0; i < keywords.size(); i++) {
        if (keywords[i] == dato) {
            encontrado = true;
            break;  // Salimos del bucle una vez que se encuentre el elemento
        }
    }
  return encontrado;
}

bool saberSiFunciones(string dato){
  bool encontrado = false;
  for (int i = 0; i < nom_funciones.size(); i++) {
        if (nom_funciones[i] == dato) {
            encontrado = true;
            break;  // Salimos del bucle una vez que se encuentre el elemento
        }
    }
  return encontrado;
}

bool funSaberSimbolo(char dato){
  bool encontrado = false;
  for (int i = 0; i < simbolos.size(); i++) {
        if (simbolos[i] == dato) {
            encontrado = true;
            break;  // Salimos del bucle una vez que se encuentre el elemento
        }
    }
  return encontrado;
}



int main() {
   std::ifstream archivo("codigoTest.txt");

    // Verifica si el archivo se abrió correctamente
    if (!archivo.is_open()) {
        std::cerr << "Error al abrir el archivo." << std::endl;
        return 1;
    }

    std::string linea;
    int linea_ubicacion = 1;
    // Lee el archivo línea por línea
    while (getline(archivo, linea)) {

      if(!linea.empty()){
        int indice=0;
        while(indice < linea.length()){
        //indice al recorrer un alinea de codigo


          //si es un simbolo
          if(linea[indice] == '>'){
            cout<<"ES UNA ASIGNACION\t"<<linea[indice]<<"\tEN LA LINEA "<<linea_ubicacion<< "EN LA POSICION ("<<indice<< ")"<<endl;
            indice++;
          }

            else{

            if(linea[indice] == '"'){
              string var = "";
              int ubi_inicio=indice;
              var+= linea[indice];
              indice++;
              while(linea[indice] != '"' ){
                var+= linea[indice];
                indice++;
              }
              var+= linea[indice];
              indice++;
              int ubi_final = indice-1;
              cout<<"ES UN STRING\t"<<var<<"\tEN LA LINEA "<<linea_ubicacion<< "\tEN LA POSICION ("<< ubi_inicio<<" : "<< ubi_final<< ")"<<endl;
            }

            if(funSaberSimbolo(linea[indice])){
              cout<<"ES UN SIMBOLO\t"<<linea[indice]<<"\tEN LA LINEA "<<linea_ubicacion<< "\tEN LA POSICION ("<< indice<< ")"<<endl;
              indice++;
            }

            if(isdigit(linea[indice])){
              string numero;
              int ubi_inicio=indice;
              while(linea[indice] != ' ' && isdigit(linea[indice])){
                numero+= linea[indice];
                indice++;
              }
              int ubi_final = indice-1;
    
              cout<<"ES UN DIGITO\t"<<numero<<"\tEN LA LINEA "<<linea_ubicacion<< "\tEN LA POSICION ("<< ubi_inicio<<" : "<< ubi_final<< ")"<<endl;
            }

            else{
              
            //si es una keyword o id
            if (std::isalpha(linea[indice])) {
              string var2 = "";
              int ubi_inicio=indice;
              while(linea[indice] != ' '){
                var2+= linea[indice];
                indice++;
              }
    
              int ubi_final = indice-1;
    
              if(saberSiKeyword(var2)){
                cout<<"ES UNA PALABRA RESERVADA\t"<<var2<<"\tEN LA LINEA "<<linea_ubicacion<< "\tEN LA POSICION ("<< ubi_inicio<<" : "<< ubi_final<< ")"<<endl;
              }
              else{

                if(saberSiFunciones(var2)){
                  cout<<"ES UNA FUNCION\t"<<var2<<"\tEN LA LINEA "<<linea_ubicacion<< "\tEN LA POSICION ("<< ubi_inicio<<" : "<< ubi_final<< ")"<<endl;
                }
                else{
                  cout<<"ES UN ID\t"<<var2<<"\tEN LA LINEA "<<linea_ubicacion<< "\tEN LA POSICION ("<< ubi_inicio<<" : "<< ubi_final<< ")"<<endl;
                }
              }
              
            }
            
             //si es espacio en blanco
            

            else{
              indice++;
            }
            }
            
  
            }
        }
        
        
      }

      linea_ubicacion++;
    }

    // Cierra el archivo cuando hayas terminado de usarlo
    archivo.close();

  
}
