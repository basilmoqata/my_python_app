def add_book(library_system):
    print("\n--- إضافة كتاب جديد ---")
    title = input("أدخل عنوان الكتاب (Title): ").strip()
    author = input("أدخل اسم المؤلف (Author): ").strip()
    year = input("أدخل سنة النشر (Year): ").strip()
    
    library_system[title] = {
        "author": author,
        "year": year
    }
    print(f"تم إضافة الكتاب '{title}' بنجاح!")

def search_book(library_system):
    print("\n--- البحث عن كتاب ---")
    search_title = input("أدخل عنوان الكتاب للبحث عنه: ").strip()
    
    if search_title in library_system:
        print(f"\n الكتاب موجود!")
        print(f"عنوان الكتاب: {search_title}")
        print(f"المؤلف: {library_system[search_title]['author']}")
        print(f"سنة النشر: {library_system[search_title]['year']}")
    else:
        print(f"\n عذراً، الكتاب '{search_title}' غير موجود في المكتبة.")

def main():
    my_library = {}
    
    while True:
        print("\n=== نظام إدارة المكتبة المصغر ===")
        print("1. إضافة كتاب جديد")
        print("2. البحث عن كتاب")
        print("3. عرض كافة الكتب")
        print("4. الخروج")
        
        choice = input("اختر العمليات (1-4): ").strip()
        
        if choice == '1':
            add_book(my_library)
        elif choice == '2':
            search_book(my_library)
        elif choice == '3':
            print("\n--- قائمة الكتب في المكتبة ---")
            if not my_library:
                print("المكتبة فارغة حالياً.")
            else:
                for t, details in my_library.items():
                    print(f"- {t} (المؤلف: {details['author']}, السنة: {details['year']})")
        elif choice == '4':
            print("شكراً لاستخدام نظام المكتبة، مع السلامة!")
            break
        else:
            print("اختيار خاطئ، يرجى إدخال رقم بين 1 و 4.")

if __name__ == "__main__":
    main()