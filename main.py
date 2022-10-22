import tkinter.messagebox
import pandas
from tkinter import *
from tkinter import ttk
import random
from gem_gen_data import gem_details

PARTY_LEVEL = 5

if PARTY_LEVEL < 5:
    tier_of_play = "under 5"
elif PARTY_LEVEL < 10:
    tier_of_play = "under 10"
elif PARTY_LEVEL < 15:
    tier_of_play = "under 15"
else:
    tier_of_play = "over 15"
print(tier_of_play)


class GemGenerator:
    """This class will manage the Gem Generator program."""

    def __init__(self):
        # Set up the gem lists from the data provided.
        self.common_gems = []
        self.uncommon_gems = []
        self.rare_gems = []
        self.very_rare_gems = []
        self.gems = []
        self.game_tier = tier_of_play
        self.generate_gem_lists()
        self.num_gems = 0
        self.rarity = ""
        self.gem_text = ""
        self.die_values = ['Selected Number', 'd4', 'd6', 'd8', 'd10', 'd12', 'd20', 'd100']

        # Set up the Tkinter GUI
        self.window = Tk()
        self.window.title("Gem Identification!")
        self.window.config(height=600, width=800)
        # Entries
        self.number_entry = Entry()
        self.number_entry.config(highlightthickness=0, width=23)
        self.number_entry.grid(column=0, row=2, pady=10, padx=10)
        self.number_entry.insert(END, "Num Gems / Num Rolls")

        # Combobox
        self.drop = ttk.Combobox(self.window, values=self.die_values, width=18)
        self.drop.grid(column=1, row=2)

        # Label
        self.title = Label()
        self.title.config(text='Gem Identification', fg='Black', font=("Birch std", 26, 'bold'))
        self.title.grid(column=0, columnspan=2, row=0)

        # Buttons
        self.generate_button = Button()
        self.generate_button.config(width=20, text="Generate Gems!", font=("Birch std", 12, 'italic'),
                                    height=1, command=self.main_code)
        self.generate_button.grid(column=0, columnspan=2, row=3, padx=10, pady=10)

        # Canvas Details
        self.canvas = Canvas(width=225, height=225, highlightthickness=0)
        image = PhotoImage(file='gem_picture.png')
        self.canvas.create_image(117, 117, image=image)
        self.canvas.grid(column=0, columnspan=2, row=1)

        self.window.mainloop()

    def generate_gem_lists(self):
        """
        Method to Generate gem lists from data provided in csv file
        This method will run on class intialisation
            """
        gem_data = pandas.read_csv("D&D 5e Gems.csv")
        gem_dictionary = gem_data.to_dict('records')
        for gem in gem_dictionary:
            if gem['Rarity'] == 'Common':
                self.common_gems.append(gem)
            elif gem['Rarity'] == 'Uncommon':
                self.uncommon_gems.append(gem)
            elif gem['Rarity'] == 'Rare':
                self.rare_gems.append(gem)
            elif gem['Rarity'] == 'Very Rare':
                self.very_rare_gems.append(gem)

    def open_popup(self):
        top = Toplevel(self.window)
        top.geometry("500x500")
        top.title("Gem List")
        Label(top, text=f"{self.gem_text}", font=('Mistral 18 bold')).place(x=150, y=80)


    def get_number_of_gems(self):
        die_value = 0
        self.num_gems = 0
        try:
            if self.drop.get() == 'Selected Number':
                self.num_gems = int(self.number_entry.get())
            else:
                rolls = int(self.number_entry.get())
                if self.drop.get() == 'd4':
                    die_value = 4
                elif self.drop.get() == 'd6':
                    die_value = 6
                elif self.drop.get() == 'd8':
                    die_value = 8
                elif self.drop.get() == 'd10':
                    die_value = 10
                elif self.drop.get() == 'd20':
                    die_value = 20
                elif self.drop.get() == 'd100':
                    die_value = 100
                for roll in range(0, rolls):
                    roll = random.randint(1, die_value)
                    self.num_gems += roll
        except:
            tkinter.messagebox.showerror("Number of rolls", "Please insert the number of die to be rolled.")
        print(self.num_gems)

    def identify_rarity(self):
        """Identifies the rariety of a particular gem."""
        rarity_chance = random.randint(0, 100)
        for key, value in gem_details[tier_of_play]["rarity"].items():
            if rarity_chance >= value:
                self.rarity = key

    def identify_type(self):
        """Randomly selects a gem from the rarity list matching generated rarity value."""
        if self.rarity == 'Common':
            chosen_gem = random.choice(self.common_gems)
            return chosen_gem
        elif self.rarity == 'Uncommon':
            chosen_gem = random.choice(self.uncommon_gems)
            return chosen_gem
        elif self.rarity == 'Rare':
            chosen_gem = random.choice(self.rare_gems)
            return chosen_gem
        else:
            chosen_gem = random.choice(self.very_rare_gems)
            return chosen_gem

    def identify_quality(self):
        """Chooses the quality of the gem based on rarity and tier of play."""
        quality_chance = random.randint(0, 100)
        for key, value in gem_details[tier_of_play][self.rarity].items():
            if quality_chance <= value:
                quality = key
                return quality

    def display_gem_details(self, gem_type, gem_quality):
        """
        Displays the details of the gem(s) identified
        Information provided in text string.
        """
        gem_description = gem_type['Description']
        gem_name = gem_type['Gem']
        gem_value = gem_type[gem_quality]
        self.gem_text += f"Gem Name: {gem_name}\nGem Description: {gem_description}" \
                         f"\nGem Value: {gem_value}\n\n"

    def main_code(self):
        """The code that brings the various Methods together when the command is received"""
        self.gems.clear()
        self.get_number_of_gems()
        self.gem_text = ""
        for gem in range(0, self.num_gems):
            self.identify_rarity()
            gem_type = self.identify_type()
            self.gems.append(gem)
            gem_quality = self.identify_quality()
            self.display_gem_details(gem_type=gem_type, gem_quality=gem_quality)
        with open("Gem List", 'w') as file:
            file.write(f"{self.gem_text}")
        print(self.gem_text)
        # self.open_popup()
        tkinter.messagebox.showinfo(title="Gem Information", message=self.gem_text)


GemGenerator()
