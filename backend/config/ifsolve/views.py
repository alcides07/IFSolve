from django.http import request
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from .permissions import IsElaborador, IsAluno
from .models import (Alternativa, Aluno, Area, Avaliacao, Elaborador, Item, ItemAvaliacao, Resposta, Tag, Usuario)
from .serializers import (AlternativaSerializer, AlunoSerializer, AreaSerializer, AvaliacaoSerializer, ElaboradorSerializer, ItemSerializer, ItemAvaliacaoSerializer, RespostaSerializer, TagSerializer, UsuarioSerializer)

class CadastroAlunoViewSet(viewsets.ModelViewSet):
    queryset = Aluno.objects.none()
    serializer_class = AlunoSerializer
    
    @action(detail=False, methods=['post'], url_path = "cadastro")
    def post(self, request):
        serializer = AlunoSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CadastroElaboradorViewSet(viewsets.ModelViewSet):
    queryset = Elaborador.objects.none()
    serializer_class = ElaboradorSerializer
    
    @action(detail=False, methods=['post'], url_path = "cadastro")
    def post(self, request):
        serializer = ElaboradorSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.none()
    serializer_class = ItemSerializer

    def retrieve(self, request, pk=None):
        #Reescrevendo método de recuperação de um item
        queryset = Item.objects.all()
        item = get_object_or_404(queryset, pk=pk)
        serializer = ItemSerializer(item)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], permission_classes=[IsAluno], url_path='aluno')
    def alunoItens(self, request, pk = None):
        #View para o aluno ver todos os itens públicos
        item = Item.objects.filter(visibilidade = 'PU') 
        serializer = ItemSerializer(item, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], permission_classes=[IsElaborador], url_path='elaborador')
    def elaboradorItens(self, request, pk = None):
        # View para o elaborador ver os itens que ele criou
        item = Item.objects.filter(elaborador=request.user.usuario.elaborador)
        serializer = ItemSerializer(item, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'], url_path='elaborador/criar', permission_classes=[IsElaborador])
    def criarItem(self, request, pk = None):
        # View para o elaborador criar um item
        serializer = ItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(elaborador=request.user.usuario.elaborador)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RespostaItemViewSet(viewsets.ModelViewSet):
    queryset = Resposta.objects.none()
    serializer_class = RespostaSerializer

    # @action(detail=True, methods=['get'], permission_classes=[IsAluno])
    @action(detail=True, methods=['get'])
    def resposta(self, request, pk=None):
        item = get_object_or_404(Item, pk=pk)
        respostas = Resposta.objects.filter(item=item, aluno=request.user.usuario.aluno)
        serializer = RespostaSerializer(respostas, many=True)
        return Response(serializer.data)