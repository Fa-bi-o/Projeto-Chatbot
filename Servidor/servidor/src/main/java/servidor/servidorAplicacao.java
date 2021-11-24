package servidor;

import javax.jws.WebService;
import java.util.HashMap;
import java.util.Map;

@WebService(targetNamespace = "http://servidor/", portName = "servidorAplicacaoPort", serviceName = "servidorAplicacaoService")
public class servidorAplicacao {
	
	class Item {
		
		String nome;
		int quantidade;
		double preco;
		
		Item (String nome, int quantidade, double preco){
			this.nome = nome;
			this.quantidade = quantidade;
			this.preco = preco;
		}

		public String getNome() {
			return nome;
		}

		public void setNome(String nome) {
			this.nome = nome;
		}

		public int getQuantidade() {
			return quantidade;
		}

		public void setQuantidade(int quantidade) {
			this.quantidade = quantidade;
		}

		public double getPreco() {
			return preco;
		}

		public void setPreco(double preco) {
			this.preco = preco;
		}	
		
		
	}
		
	public int verificarEstoque(String nome) {
				
		Map<String, Item> estoque = new HashMap<String, Item>();	
		
		estoque.put("Sanduiche", new Item("Feijão", 2, 15.00));
		estoque.put("Hamburguer", new Item("Hamburguer", 0, 23.00));
		estoque.put("Batata Frita", new Item("Batata Frita", 5, 6.00));
		estoque.put("Refrigerante", new Item("Refrigerante", 3, 8.00));
		estoque.put("Suco", new Item("Suco", 10, 6.00));
			
		int quantidade = 0; 
			
		if (estoque.containsKey(nome)) {
			quantidade = estoque.get(nome).getQuantidade();
		}
			
		return quantidade;
	}
	
	public double calcularPreco(String[] nome) {
		
		Map<String, Item> estoque = new HashMap<String, Item>();	
		
		estoque.put("Sanduiche", new Item("Feijão", 2, 15.00));
		estoque.put("Hamburguer", new Item("Hamburguer", 0, 23.00));
		estoque.put("Batata Frita", new Item("Batata Frita", 5, 6.00));
		estoque.put("Refrigerante", new Item("Refrigerante", 3, 8.00));
		estoque.put("Suco", new Item("Suco", 10, 6.00));
			
		double total = 0;
		
		for (int i = 0; i < nome.length; i++) {
			
			if (estoque.containsKey(nome[i])) {
				total = total + estoque.get(nome[i]).getPreco();
			}
		}	
		
		return total;
	}
}
