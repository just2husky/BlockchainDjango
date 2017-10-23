#!/usr/bin/python3
# -*- coding: UTF-8 -*-
from django.shortcuts import render_to_response, render
from ..service.block_chain_service import BlockChainService


def block_chain_init(request):
    ctx = {}
    last_block_id = BlockChainService.init()
    ctx['msg'] = '初始化区块链成功，初始区块ID为：' + last_block_id
    return render(request, 'blockchain_manager.html', ctx)


def block_chain_manager(request):
    return render_to_response('blockchain_manager.html')
