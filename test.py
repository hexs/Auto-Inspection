
    elif event.type == pygame.TEXTINPUT:
        if event.dict['text'] == 'd':
            self.start_pos = self.start_pos[0] + 10, self.start_pos[1]
            self.end_pos = self.end_pos[0] + 10, self.end_pos[1]
        elif event.dict['text'] == 'a':
            self.start_pos = self.start_pos[0] - 10, self.start_pos[1]
            self.end_pos = self.end_pos[0] - 10, self.end_pos[1]
        elif event.dict['text'] == 'w':
            self.start_pos = self.start_pos[0], self.start_pos[1] - 10
            self.end_pos = self.end_pos[0], self.end_pos[1] - 10
        elif event.dict['text'] == 's':
            self.start_pos = self.start_pos[0], self.start_pos[1] + 10
            self.end_pos = self.end_pos[0], self.end_pos[1] + 10