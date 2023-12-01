from utils import config
from utils.splash_screen import SplashScreen
from reports.relatorios import Relatorio
from controller.controller_paciente import Controller_Paciente
from controller.controller_profissional import Controller_Profissional
from controller.controller_agendamento import Controller_Agendamento

def exibir_menu(opcoes, mensagem):
    print(opcoes)
    return int(input(mensagem))

def exibir_relatorio(relatorio, opcao_relatorio):
    relatorio_funcoes = {
        1: relatorio.get_relatorio_agendamentos,
        2: relatorio.get_relatorio_pacientes,
        3: relatorio.get_relatorio_profissionais,
    }
    relatorio_funcoes.get(opcao_relatorio, lambda: None)()

def executar_acao(controller, relatorio, opcao, acao):
    relatorio_funcoes = {
        1: relatorio.get_relatorio_pacientes,
        2: relatorio.get_relatorio_profissionais,
        3: relatorio.get_relatorio_agendamentos,
    }
    relatorio_funcoes.get(opcao, lambda: None)()
    acao()

def run():
    tela_inicial = SplashScreen()
    relatorio = Relatorio()
    ctrl_paciente = Controller_Paciente()
    ctrl_profissional = Controller_Profissional()
    ctrl_agendamento = Controller_Agendamento()

    print(tela_inicial.get_updated_screen())
    config.clear_console()

    while True:
        opcao_principal = exibir_menu(config.MENU_PRINCIPAL, "Escolha uma opção [1-5]: ")
        config.clear_console(1)

        if opcao_principal == 5:
            print(tela_inicial.get_updated_screen())
            config.clear_console()
            print("Obrigado por utilizar o nosso sistema.")
            exit(0)

        if 1 <= opcao_principal <= 4:
            opcao_entidades = exibir_menu(config.MENU_ENTIDADES, "Escolha uma opção [1-3]: ")
            config.clear_console(1)

            if 1 <= opcao_entidades <= 3:
                if opcao_principal == 1:
                    exibir_relatorio(relatorio, opcao_entidades)

                elif opcao_principal == 2:
                    executar_acao(
                        ctrl_paciente,
                        relatorio,
                        opcao_entidades,
                        ctrl_paciente.inserir_paciente,
                    )

                elif opcao_principal == 3:
                    executar_acao(
                        ctrl_paciente,
                        relatorio,
                        opcao_entidades,
                        ctrl_paciente.atualizar_paciente,
                    )

                elif opcao_principal == 4:
                    executar_acao(
                        ctrl_paciente,
                        relatorio,
                        opcao_entidades,
                        ctrl_paciente.excluir_paciente,
                    )

                print(tela_inicial.get_updated_screen())
                config.clear_console()

            else:
                print("Opção incorreta.")
                exit(1)

if __name__ == "__main__":
    run()
