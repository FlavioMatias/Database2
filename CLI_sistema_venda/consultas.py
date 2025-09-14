from enum import Enum

class Consulta(Enum):
    USUARIOS_ATIVOS = (
        """
        SELECT id_usuario, nome, email, telefone
        FROM usuario
        WHERE ativo = TRUE;
        """,
        "1. Listagem de Usuários Ativos"
    )
    
    PRODUTOS_CATEGORIA = (
        """
        SELECT nome, preco, quantidade_estoque
        FROM produto
        WHERE categoria = 'Informática'
        ORDER BY preco ASC;
        """,
        "2. Catálogo de Produtos por Categoria"
    )
    
    PEDIDOS_STATUS = (
        """
        SELECT status_pedido, COUNT(*) AS total_pedidos
        FROM pedido
        GROUP BY status_pedido;
        """,
           
        "3. Contagem de Pedidos por Status"
    )
    
    ESTOQUE_BAIXO = (
        """
        SELECT nome, categoria, quantidade_estoque
        FROM produto
        WHERE quantidade_estoque < 30;
        """,
        "4. Alerta de Estoque Baixo"
    )
    
    PEDIDOS_RECENTES = (
        """
        SELECT id_pedido as id, TO_CHAR(data_pedido, 'DD/MM/YYYY') AS data, valor_total as valor, status_pedido as status
        FROM pedido
        WHERE data_pedido >= CURRENT_DATE - INTERVAL '60 day';
           """,
        "5. Histórico de Pedidos Recentes"
    )
    
    PRODUTOS_CAROS_CATEGORIA = (
        """
        SELECT categoria, nome, preco
           FROM (
               SELECT 
                   categoria,
                   nome,
                   preco,
                   ROW_NUMBER() OVER (PARTITION BY categoria ORDER BY preco DESC) AS rn
               FROM produto
           ) t
           WHERE rn = 1;
        """,
        "6. Produtos Mais Caros por Categoria"
    )
   
    CONTATOS_INCOMPLETOS = (
        '''
            SELECT *
            FROM usuario
            WHERE ativo = true and telefone IS NULL;
        ''',
        "7. Clientes com Dados de Contato Incompletos"
    )
    
    PEDIDOS_ENVIADOS = (
        """
        SELECT u.nome, u.email, u.telefone, p.endereco_entrega
        FROM pedido as p
        JOIN usuario as u
            ON p.id_usuario = u.id_usuario
        WHERE p.status_pedido = 'enviado';
        """,
        "8. Pedidos Pendentes de Entrega"
    )
    
    DETALHAMENTO_PEDIDO = (
        """
            SELECT u.nome as nome_cliente, u.telefone as telefone_cliente, u.email as email_cliente,
                pr.nome as nome_produto, pr.categoria as categoria_produto, pr.peso as peso_produto,
                ip.quantidade, ip.preco_unitario, ip.subtotal
            FROM pedido AS pe
            JOIN usuario AS u ON pe.id_usuario = u.id_usuario
            JOIN itens_pedido AS ip ON pe.id_pedido = ip.id_pedido
            JOIN produto AS pr ON pr.id_produto = ip.id_produto
            WHERE pe.id_pedido = 1;
        """,
        "9. Detalhamento Completo de Pedidos"
    )
    
    RANKING_PRODUTOS = (
        """
        SELECT 
            pr.nome,
            pr.categoria,
            SUM(ip.quantidade) AS total_vendido
        FROM produto AS pr
        JOIN itens_pedido AS ip
            ON pr.id_produto = ip.id_produto
        GROUP BY pr.id_produto, pr.nome, pr.categoria
        ORDER BY total_vendido DESC;

        """,
        "10. Ranking dos Produtos Mais Vendidos"
    )
    
    CLIENTES_SEM_COMPRAS = (
        """
        SELECT u.*
        FROM usuario AS u
        WHERE u.ativo = true AND NOT EXISTS (SELECT NULL
                                             FROM pedido AS p
                                             WHERE p.id_usuario = u.id_usuario);
        """,
        "11. Análise de Clientes Sem Compras"
    )
    
    ESTATISTICAS_CLIENTE = (
        """
        SELECT 
            u.id_usuario,
            u.nome,
            COUNT(p.id_pedido) AS total_pedidos,
            AVG(p.valor_total) AS valor_medio_pedido,
            SUM(p.valor_total) AS valor_total_gasto
        FROM usuario AS u
        JOIN pedido AS p
            ON u.id_usuario = p.id_usuario
        GROUP BY u.id_usuario, u.nome
        ORDER BY valor_total_gasto DESC;

        
        """,
        "12. Estatísticas de Compras por Cliente"
    )
    
    RELATORIO_MENSAL = (
        """
        SELECT 
            TO_CHAR(p.data_pedido, 'MM/YYYY') AS periodo,
            COUNT(DISTINCT p.id_pedido)       AS quantidade_pedidos,
            COUNT(DISTINCT ip.id_produto)     AS produtos_diferentes,
            SUM(ip.quantidade * ip.preco_unitario) AS faturamento_total
        FROM pedido AS p
        JOIN itens_pedido AS ip 
            ON p.id_pedido = ip.id_pedido
        GROUP BY TO_CHAR(p.data_pedido, 'MM/YYYY')
        ORDER BY MIN(p.data_pedido);
        """,
        "13. Relatório Mensal de Vendas"
    )
    
    PRODUTOS_NAO_VENDIDOS = (
        """
        SELECT pr.*
        FROM produto AS pr
        WHERE pr.ativo = true
            AND NOT EXISTS (
                SELECT NULL
                FROM itens_pedido AS ip
                WHERE ip.id_produto = pr.id_produto
            );

        """,
        "14. Produtos que Nunca Foram Vendidos"
    )
    
    TICKET_MEDIO_CATEGORIA = (
        """
        SELECT 
            sub.categoria,
            AVG(sub.total_pedido) AS ticket_medio
        FROM (
            SELECT 
                pe.id_pedido,
                p.categoria,
                SUM(ip.quantidade * ip.preco_unitario) AS total_pedido
            FROM pedido AS pe
            JOIN itens_pedido AS ip ON ip.id_pedido = pe.id_pedido
            JOIN produto AS p ON p.id_produto = ip.id_produto
            WHERE pe.status_pedido <> 'cancelado'
            GROUP BY pe.id_pedido, p.categoria
        ) AS sub
        GROUP BY sub.categoria
        ORDER BY ticket_medio DESC;
        """,
        "15. Análise de Ticket Médio por Categoria"
    )
