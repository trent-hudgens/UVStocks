from ctypes import alignment
from tkinter import *
#from PIL import Image, ImageTK




def main():
    root = Tk()

    root.title("UVStocks")

    #positioning and sizes
    #Each element's Y position is based on the Y position and height of the element above it
    spacing = 25
    rootWidth = 550
    rootHeight = 625
    logoWidth = 100
    logoHeight = 50
    logoX = rootWidth/2 - logoWidth/2
    logoY = spacing
    frameStockWidth = rootWidth - spacing*2
    frameStockHeight = rootHeight - spacing*2 - logoHeight - spacing
    frameStockX = spacing
    frameStockY = logoY + logoHeight + spacing
    textCashWidth = 100
    textCashHeight = 25
    textCashX = frameStockX + spacing
    textCashY = frameStockY
    textSharesWidth = 150
    textSharesHeight = 25
    textSharesX = frameStockX + frameStockWidth - textSharesWidth - spacing
    textSharesY = frameStockY
    graphWidth = frameStockWidth
    graphHeight = 300
    graphX = frameStockX
    graphY = textCashY + textCashHeight
    btnBuyWidth = 150
    btnBuyHeight = 50
    btnBuyX = frameStockX
    btnBuyY = graphY + graphHeight + spacing
    btnSellWidth = 150
    btnSellHeight = 50
    btnSellX = frameStockX + frameStockWidth - btnSellWidth - spacing
    btnSellY = graphY + graphHeight + spacing
    inputAmountWidth = frameStockWidth
    inputAmountHeight = 25
    inputAmountX = frameStockX
    inputAmountY = btnBuyY + btnBuyHeight + spacing
    scoreWidth = 400
    scoreHeight = 25
    scoreX = frameStockX
    scoreY = inputAmountY + inputAmountHeight + spacing


    root.configure(background="black", width=rootWidth, height=rootHeight)

    #uvstocks logo
    logo = PhotoImage(file="UVStock.png")
    #logo = logo.resize(100,100)
    Label(root, image=logo, bg="black", fg="white").place(width=logoWidth, height=logoHeight, x = logoX, y = logoY)

    frameStock= Frame(root, bg="black").place(width=frameStockWidth, height=frameStockHeight,  x = frameStockX, y = frameStockY)
    Label(frameStock, text="Total Cash: xxx", bg="black", fg="white", anchor="w").place(width=textCashWidth, height=textCashHeight, x = textCashX, y = textCashY)
    Label(frameStock, text="Total Shares Held: xxx", bg="black", fg="white", anchor="e").place(width=textSharesWidth, height=textSharesHeight, x = textSharesX, y = textSharesY)
    sampleGraph = PhotoImage(file="sampleGraph.png")
    Label(frameStock, image=sampleGraph, bg="black", fg="white").place(width=graphWidth, height=graphHeight, x = graphX, y = graphY)
    Button(frameStock, text="Buy Now!", bg="green", fg="white").place(width = btnBuyWidth, height = btnBuyHeight, x = btnBuyX, y = btnBuyY)
    Button(frameStock, text="Sell Now!", bg="red", fg="white").place(width = btnSellWidth, height = btnSellHeight, x = btnSellX, y = btnSellY)

    #entry field for amount of stocks to buy or sell
    inputAmount = Entry(frameStock, bg="white", fg="black")
    inputAmount.place(width = inputAmountWidth, height = inputAmountHeight, x = inputAmountX, y = inputAmountY)
    inputAmount.insert(0, "Amount")
    def clickInput(*args):
        inputAmount.delete(0, 'end')
    def focusOutInput(*args):
        amountStr = str(inputAmount.get())
        if amountStr == "":
            inputAmount.insert(0, "Amount")
            root.focus()
    inputAmount.bind("<Button-1>", clickInput)
    inputAmount.bind("<FocusOut>", focusOutInput)

    Label(frameStock, text="SCORE: XXXXX.XX", bg="black", fg="white", anchor="w").place(width=scoreWidth, height=scoreHeight, x = scoreX, y = scoreY)

    root.mainloop()


if __name__ == "__main__":
    main()