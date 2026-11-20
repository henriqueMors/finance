# CSS da faixa rolante (carrossel)
CSS_FAIXA = """
<style>
.faixa { overflow: hidden; white-space: nowrap; padding: 8px 0;
         border-top: 1px solid rgba(128,128,128,.3);
         border-bottom: 1px solid rgba(128,128,128,.3); }
.trilho { display: inline-block; animation: rolar linear infinite; }
.faixa:hover .trilho { animation-play-state: paused; }
.item { margin: 0 40px; font-size: 1.05rem; }
@keyframes rolar { from { transform: translateX(0); }
                   to   { transform: translateX(-50%); } }
</style>
"""

COR_ALTA = "#21c354"
COR_BAIXA = "#ff4b4b"
