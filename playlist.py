class Song:
    def __init__(self, title):
        self.title = title
        self.next = None
        self.prev = None

class Playlist:
    def __init__(self):
        self.head = None
        self.tail = None
        self.current = None

    def add_song_end(self, title):
        new_song = Song(title)
        if not self.head:
            self.head = new_song
            self.tail = new_song
            self.current = new_song
        else:
            new_song.prev = self.tail
            self.tail.next = new_song
            self.tail = new_song

    def add_song_start(self, title):
        new_song = Song(title)
        if not self.head:
            self.head = new_song
            self.tail = new_song
            self.current = new_song
        else:
            new_song.next = self.head
            self.head.prev = new_song
            self.head = new_song

    def add_song_after(self, current_title, new_title):
        current = self.head
        while current:
            if current.title == current_title:
                new_song = Song(new_title)
                new_song.prev = current
                new_song.next = current.next
                if current.next:
                    current.next.prev = new_song
                current.next = new_song
                if current == self.tail:
                    self.tail = new_song
                break
            current = current.next

    def remove_song(self, title):
        current = self.head
        while current:
            if current.title == title:
                if current.prev:
                    current.prev.next = current.next
                else:
                    self.head = current.next

                if current.next:
                    current.next.prev = current.prev
                else:
                    self.tail = current.prev

                # Update current if the removed song was the current song
                if current == self.current:
                    self.current = current.next or current.prev
                break
            current = current.next

    def next_song(self):
        if self.current and self.current.next:
            self.current = self.current.next

    def previous_song(self):
        if self.current and self.current.prev:
            self.current = self.current.prev

    def display_playlist(self):
        if not self.head:
            print("The playlist is empty.")
            return
        
        current = self.head
        print("Playlist:")
        while current:
            marker = " <-- Current song" if current == self.current else ""
            print(f"{current.title}{marker}")
            current = current.next

    def get_current_song(self):
        return self.current.title if self.current else "No songs in playlist"

def main():
    playlist = Playlist()
    
    while True:
        print("\n--- Playlist Menu ---")
        print("1. Add song to end")
        print("2. Add song to start")
        print("3. Add song after another")
        print("4. Remove song")
        print("5. Next song")
        print("6. Previous song")
        print("7. Show playlist")
        print("8. Current song")
        print("9. Exit")
        
        option = input("Choose an option (1-9): ")
        
        if option == '1':
            title = input("Enter the song title: ")
            playlist.add_song_end(title)
        elif option == '2':
            title = input("Enter the song title: ")
            playlist.add_song_start(title)
        elif option == '3':
            current_title = input("After which song do you want to add: ")
            new_title = input("Enter the new song title: ")
            playlist.add_song_after(current_title, new_title)
        elif option == '4':
            title = input("Enter the song title to remove: ")
            playlist.remove_song(title)
        elif option == '5':
            playlist.next_song()
        elif option == '6':
            playlist.previous_song()
        elif option == '7':
            playlist.display_playlist()
        elif option == '8':
            print("Current song:", playlist.get_current_song())
        elif option == '9':
            print("Goodbye!")
            break
        else:
            print("Invalid option. Try again.")

if __name__ == "__main__":
    main()
