from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.clock import Clock
import random

class SlotMachineApp(App):
    def build(self):
        self.total_bet = 0
        self.max_bet = 100
        self.total_win = 0

        main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Bet amount input
        bet_layout = BoxLayout(orientation='horizontal', size_hint=(1, None), height=40)
        self.bet_input = TextInput(text="0", multiline=False, font_size=24, size_hint=(0.6, 1))
        bet_layout.add_widget(Label(text="Bet Amount:", font_size=24, size_hint=(0.4, 1)))
        bet_layout.add_widget(self.bet_input)
        main_layout.add_widget(bet_layout)

        # Reel images (using placeholder images)
        self.reel_images = []
        reel_layout = GridLayout(cols=3, size_hint=(1, None), height=300, spacing=10)
        for _ in range(9):
            reel_image = Image(source='DIAMOND.png') 
            reel_layout.add_widget(reel_image)
            self.reel_images.append(reel_image)
        main_layout.add_widget(reel_layout)

        # Spin button
        self.spin_button = Button(text="Spin", font_size=32, size_hint=(1, None), height=60)
        self.spin_button.bind(on_press=self.start_spin)
        main_layout.add_widget(self.spin_button)

        # Info labels
        info_layout = GridLayout(cols=2, size_hint=(1, None), height=120)
        self.win_label = Label(text="Win: 0", font_size=20)
        self.total_bet_label = Label(text="Total Bet: 0", font_size=20)
        self.max_bet_label = Label(text="Max Bet: 100", font_size=20)
        self.total_win_label = Label(text="Total Win: 0", font_size=20)
        
        info_layout.add_widget(self.win_label)
        info_layout.add_widget(self.total_bet_label)
        info_layout.add_widget(self.max_bet_label)
        info_layout.add_widget(self.total_win_label)
        main_layout.add_widget(info_layout)

        return main_layout

    def start_spin(self, instance):
        try:
            self.bet_amount = float(self.bet_input.text)
        except ValueError:
            self.show_popup("Invalid Bet", "Please enter a valid number.")
            return

        if self.bet_amount > self.max_bet or self.bet_amount < 0.5:
            self.show_popup("Invalid Bet", "Bet amount must be between 0.5 and 100.")
        else:
            self.spin_button.disabled = True
            self.cycle_count = 0
            self.cycle_images()
    #Cycle the images
    def cycle_images(self, dt=None):
        if self.cycle_count < 10:
            for reel_image in self.reel_images:
                random_image = random.choice(['DIAMOND.png', 'CRYSTAL.png', 'LEMON.png', 'COIN.png', 'PEARL.png', 'HEART.png', 'BOMB.png', 'HAT.png', 'BAG.png'])
                reel_image.source = random_image
            self.cycle_count += 1
            Clock.schedule_once(self.cycle_images, 0.1)
        else:
            self.stop_spin()

    def stop_spin(self):
        reels = [reel.source for reel in self.reel_images]
        win_amount = 0

        # Check for a full screen of the same symbol
        if len(set(reels)) == 1:
            win_amount = self.bet_amount * 30
        else:
            # Check diagonals for matches
            if reels[0] == reels[4] == reels[8] or reels[2] == reels[4] == reels[6]:
                win_amount += self.bet_amount * 0.5

            # Check each column for vertical wins
            columns = [reels[i:i+7:3] for i in range(3)] 
            matching_columns = sum(1 for col in columns if len(set(col)) == 1)

            if matching_columns == 1:
                win_amount += self.bet_amount * 0.5
            elif matching_columns == 2:
                win_amount += self.bet_amount 

            # Check each row for horizontal wins
            rows = [reels[i:i+3] for i in range(0, 9, 3)]  
            matching_rows = sum(1 for row in rows if len(set(row)) == 1)

            if matching_rows == 1:
                win_amount += self.bet_amount * 0.5
            elif matching_rows == 2:
                win_amount += self.bet_amount  
              
        self.total_bet += self.bet_amount
        self.total_win += win_amount

        self.win_label.text = f"Win: {win_amount}"
        self.total_bet_label.text = f"Total Bet: {self.total_bet}"
        self.total_win_label.text = f"Total Win: {self.total_win}"

        self.spin_button.disabled = False

    def show_popup(self, title, message):
        popup_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        popup_layout.add_widget(Label(text=message, font_size=18))
        close_button = Button(text="OK", size_hint=(1, None), height=40)
        popup_layout.add_widget(close_button)

        popup = Popup(title=title, content=popup_layout, size_hint=(None, None), size=(400, 200))
        close_button.bind(on_press=popup.dismiss)
        popup.open()

if __name__ == '__main__':
    SlotMachineApp().run()
