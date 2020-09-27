import urwid

from .scroll import Scrollable


class Entry:
    pass
    
    def __init__(self):
        pass
    
    @property
    def widget(self):
        text = """On the other hand, we denounce with righteous indignation and dislike men who are so beguiled and demoralized by the charms of pleasure of the moment, so blinded by desire, that they cannot foresee the pain and trouble that are bound to ensue; and equal blame belongs to those who fail in their duty through weakness of will, which is the same as saying through shrinking from toil and pain. These cases are perfectly simple and easy to distinguish. In a free hour, when our power of choice is untrammelled and when nothing prevents our being able to do what we like best, every pleasure is to be welcomed and every pain avoided. But in certain circumstances and owing to the claims of duty or the obligations of business it will frequently occur that pleasures have to be repudiated and annoyances accepted. The wise man therefore always holds in these matters to this principle of selection: he rejects pleasures to secure other greater pleasures, or else he endures pains to avoid worse pains.
        
        On the other hand, we denounce with righteous indignation and dislike men who are so beguiled and demoralized by the charms of pleasure of the moment, so blinded by desire, that they cannot foresee the pain and trouble that are bound to ensue; and equal blame belongs to those who fail in their duty through weakness of will, which is the same as saying through shrinking from toil and pain. These cases are perfectly simple and easy to distinguish. In a free hour, when our power of choice is untrammelled and when nothing prevents our being able to do what we like best, every pleasure is to be welcomed and every pain avoided. But in certain circumstances and owing to the claims of duty or the obligations of business it will frequently occur that pleasures have to be repudiated and annoyances accepted. The wise man therefore always holds in these matters to this principle of selection: he rejects pleasures to secure other greater pleasures, or else he endures pains to avoid worse pains."
        
        On the other hand, we denounce with righteous indignation and dislike men who are so beguiled and demoralized by the charms of pleasure of the moment, so blinded by desire, that they cannot foresee the pain and trouble that are bound to ensue; and equal blame belongs to those who fail in their duty through weakness of will, which is the same as saying through shrinking from toil and pain. These cases are perfectly simple and easy to distinguish. In a free hour, when our power of choice is untrammelled and when nothing prevents our being able to do what we like best, every pleasure is to be welcomed and every pain avoided. But in certain circumstances and owing to the claims of duty or the obligations of business it will frequently occur that pleasures have to be repudiated and annoyances accepted. The wise man therefore always holds in these matters to this principle of selection: he rejects pleasures to secure other greater pleasures, or else he endures pains to avoid worse pains."
        """
        
        widgets = {}
        text = [urwid.Text(line) for line in text.splitlines()]
        captions = "ComposerView ClassicalView WorkView BasicInfo".split()
        
        items = [urwid.LineBox(urwid.Button(caption)) for caption in captions]
        
        walker = urwid.SimpleFocusListWalker(items)
        grid_flow = urwid.GridFlow(walker, cell_width=25, h_sep=1, v_sep=1, align='center')
        
        def callback(button: urwid.Button, index: int):
            frame.contents['body'] = (widgets[index], None)
        
        for index, caption in enumerate(captions):
            body = text.copy()
            body = [urwid.Text(caption), urwid.Divider(div_char='-')] + body
            info_pile = urwid.Pile(body)
            scrollable = Scrollable(info_pile)
            widgets[index] = scrollable
            urwid.connect_signal(items[index].original_widget, "click", callback, user_arg=index)

        frame = urwid.Frame(widgets[0])
        box = urwid.LineBox(frame)
        box = urwid.BoxAdapter(box, 25)
        pile = urwid.Pile([grid_flow, box])
        return urwid.Filler(pile)
       